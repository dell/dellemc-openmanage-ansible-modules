# Architecture: providers/

## Metadata

<!-- yaml-metadata-start -->
scope_paths: ["./"]
capture_git_sha: "50215ac9190c7f50bd14327ee114f8dd2ef88e5c"
status: "current"
auto_update: false
preview_before_apply: true
scaffold_version: "1.0"
<!-- yaml-metadata-end -->

---

## Purpose and Structure

`providers/` is a local workspace containing six Ansible Galaxy collections and one shared context bundle. Each collection is an independent Git repo that delivers declarative, idempotent resource management for a specific Dell hardware platform. All collections are published to Ansible Galaxy under the `dellemc` namespace.

Five of the six collections target Dell storage arrays and share a common internal layout. The sixth (`dellemc.openmanage`) targets Dell PowerEdge server lifecycle management and has a structurally distinct layout.

---

## Components

### Collection Inventory

| Sub-repo | Galaxy FQCN | Version | Modules | Python SDK | SDK Version |
|---|---|---|---|---|---|
| `ansible-powerscale/` | `dellemc.powerscale` | 3.9.1 | 56 | `isilon-sdk` | 0.6.0 (pinned) |
| `ansible-powerstore/` | `dellemc.powerstore` | 3.8.1 | 45 | `PyPowerStore` | 3.4.2 (pinned) |
| `ansible-powerflex/` | `dellemc.powerflex` | 3.0.0 | 22 | `PyPowerFlex` | 2.0.0 (pinned) |
| `ansible-powermax/` | `dellemc.powermax` | 4.0.2 | 17 | `PyU4V` | >=10.2.0.3,==10.2.0.* |
| `ansible-unity/` | `dellemc.unity` | 2.1.0 | 18 | `storops` | >=1.2.12 |
| `dellemc-openmanage-ansible-modules/` | `dellemc.openmanage` | 10.0.2 | 105 + 16 roles | `omsdk`, `netaddr` | netaddr >=0.7.19 |

### Storage Collection Layout (powerscale, powerstore, powerflex, powermax, unity)

All five share this directory layout exactly:

```
<collection>/
  galaxy.yml                          ← namespace=dellemc, name=<platform>, version
  requirements.txt                    ← pinned Python SDK (single line)
  requirements.yml                    ← Ansible collection deps (usually empty)
  meta/
    runtime.yml                       ← requires_ansible, tombstones, action_groups
    execution-environment.yml         ← EE definition (refs requirements.txt + .yml)
  plugins/
    doc_fragments/
      <platform>.py                   ← shared DOCUMENTATION fragment: connection params
    modules/
      <resource>.py                   ← one file per resource (see Module Structure below)
    module_utils/
      storage/dell/
        utils.py                      ← SDK init, connection factory, logger, error helpers
        logging_handler.py            ← CustomRotatingFileHandler (5 MB rotate, 5 backups)
        [shared_library/ or libraries/]  ← domain helpers (powerscale, powerstore, powerflex only)
  playbooks/
    modules/
      <resource>.yml                  ← example playbook per module (mandatory deliverable)
  tests/
    unit/
      plugins/
        modules/
          test_<resource>.py          ← unit test per module
        module_utils/
          mock_<platform>_api.py      ← API mock helpers
  docs/
    modules/                          ← generated RST/MD module documentation
```

### `libraries/` / `shared_library/` Layer

The three larger storage collections add a domain helper sub-directory alongside `utils.py`. The directory is named `shared_library/` in `ansible-powerscale` and `libraries/` in `ansible-powerstore` and `ansible-powerflex`. The naming differs; the purpose is identical.

| Collection | Directory name | Contents |
|---|---|---|
| `ansible-powerscale` | `shared_library/` | `powerscale_base.py` (base class) + 12 per-API-domain helpers: `auth.py`, `certificate.py`, `cluster.py`, `events.py`, `ipmi.py`, `namespace.py`, `nwpool_utils.py`*, `protocol.py`, `quota.py`, `snapshot.py`, `support_assist.py`, `synciq.py`, `zones_summary.py` |
| `ansible-powerstore` | `libraries/` | `powerstore_base.py` (base class), `configuration.py` (`ConfigurationSDK`), `provisioning.py` |
| `ansible-powerflex` | `libraries/` | `powerflex_base.py` (base class + `@powerflex_compatibility` decorator), `configuration.py` |
| `ansible-powermax` | *(none)* | No shared base; modules call `utils.get_powermax_connection()` directly |
| `ansible-unity` | *(none)* | No shared base; modules call `utils.get_unity_connection()` directly |

*`nwpool_utils.py` lives at the `storage/dell/` level, not inside `shared_library/`.

### OpenManage Layout

`dellemc-openmanage-ansible-modules/` does **not** follow the storage collection layout:

```
dellemc-openmanage-ansible-modules/
  plugins/
    modules/                          ← 105 modules (iDRAC, OME, OMEVV, Redfish)
    inventory/                        ← 1 inventory plugin (ome_inventory)
    module_utils/                     ← flat; per-API-surface clients (no storage/dell/ path)
      ome.py                          ← OpenManage Enterprise REST client
      idrac_redfish.py                ← iDRAC Redfish client
      redfish.py                      ← generic Redfish client
      rest_api.py                     ← base HTTP REST client
      omevv.py                        ← OpenManage Enterprise OMEVV client
      session_utils.py                ← session lifecycle
      dellemc_idrac.py                ← iDRAC legacy client
      idrac_utils/                    ← 35 iDRAC-specific utility helpers
      omevv_utils/                    ← 3 OMEVV-specific utility helpers
    doc_fragments/                    ← 9 shared DOCUMENTATION fragments
  roles/                              ← 16 Ansible roles (idrac_*, redfish_*)
  bindep.txt                          ← system package requirements (no storage equivalent)
  galaxy.yml                          ← cross-collection deps: ansible.utils, ansible.windows
```

---

## Key Behaviors

### Module Execution Pattern (all storage modules)

**GIVEN** a playbook declares a desired resource state using `state: present`  
**WHEN** the Ansible engine runs the module  
**THEN** the module (1) validates parameters, (2) initialises SDK client via `utils.get_<platform>_connection()`, (3) fetches current resource state via GET, (4) compares current vs desired, (5) applies no change if identical (`changed=false`), (6) applies delta via SDK PUT/POST if different, (7) returns `changed=true` + updated resource details

### Idempotency

**GIVEN** a module has been run and the resource already matches the declared state  
**WHEN** the same playbook is run again  
**THEN** the module returns `changed=false` without making any SDK write call — enforced by the GET-compare step in `perform_module_operation()`

### Check Mode

**GIVEN** `--check` is passed to `ansible-playbook`  
**WHEN** the module would normally apply a change  
**THEN** the module reports `changed=true` and the intended change but skips all SDK write calls — enforced by `if not self.module.check_mode:` guards before every POST/PUT/DELETE

### Action Group

**GIVEN** a playbook uses `module_defaults` with `group/dellemc.<platform>.all`  
**WHEN** any module in the collection is invoked  
**THEN** the shared connection parameters (`onefs_host`, `api_user`, `api_password`, `verify_ssl`, etc.) are injected without repeating them per task — the group is defined in `meta/runtime.yml` and lists every module FQCN

### Deprecated Module Redirect

**GIVEN** a legacy playbook uses the old `dellemc_powerscale_<resource>` module name  
**WHEN** the collection is executed  
**THEN** Ansible emits a deprecation warning and routes the call to the current `<resource>` module name — governed by tombstone entries in `meta/runtime.yml`

### PowerFlex Module Version Gating

**GIVEN** a PowerFlex module class is decorated with `@powerflex_compatibility(min_ver=..., max_ver=...)`  
**WHEN** the module is invoked against a PowerFlex system  
**THEN** the base class checks the running PowerFlex API version; if outside the compatible range, the task exits with `changed=false` and a skip warning naming the correct module to use instead

---

## Interfaces

### Connection Parameters (injected by `doc_fragments/<platform>.py` + `utils.get_<platform>_management_host_parameters()`)

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `onefs_host` / `array_ip` / `hostname` | str | Yes | Management IP or FQDN (naming varies by collection) |
| `api_user` / `username` | str | Yes | Platform admin credential |
| `api_password` / `password` | str | Yes | `no_log: True` always set |
| `verify_ssl` / `validate_certs` | bool | Yes | Must be `true` in production |
| `port_no` | str | No | Default `8080` (powerscale only) |

### Module Return Contract

Every module returns at minimum:

| Return key | Type | Description |
|---|---|---|
| `changed` | bool | `true` if the module made any change |
| `<resource>_details` | dict or list | Current resource state after execution; empty dict `{}` on `state: absent` |

### FQCN Invocation Pattern

```yaml
- name: <task description>
  dellemc.<platform>.<resource>:
    onefs_host: "{{ onefs_host }}"
    api_user: "{{ api_user }}"
    api_password: "{{ api_password }}"
    verify_ssl: "{{ verify_ssl }}"
    # resource-specific params
    state: present | absent
```

### Base Class Constructor Interface (powerscale, powerstore, powerflex)

All `<Platform>Base.__init__(ansible_module, ansible_module_params)` accept:
- `ansible_module`: the `AnsibleModule` class (not an instance) — injected by the module's `__init__`
- `ansible_module_params`: dict with `argument_spec`, `supports_check_mode`, etc.

The base class merges connection parameters into `argument_spec`, instantiates `AnsibleModule`, validates SDK presence, and creates the SDK client. Subclasses call `super().__init__()` and then access `self.module`, `self.result`, `self.api_client` (powerscale) / `self.conn` (powerstore) / `self.powerflex_conn` (powerflex).

---

## Dependencies

### Per-collection Python SDK

| Collection | SDK package | Import style | Version coupling |
|---|---|---|---|
| `dellemc.powerscale` | `isilon-sdk==0.6.0` | **Dynamic** — `importlib.import_module("isilon_sdk.<version>")` at runtime | Static analysis cannot detect; declared only in `requirements.txt` |
| `dellemc.powerstore` | `PyPowerStore==3.4.2` | Static import, checked at module load via `HAS_PY4PS` flag | Module fails at import if version mismatch |
| `dellemc.powerflex` | `PyPowerFlex==2.0.0` | Static import, checked via `ensure_required_libs()` | `@powerflex_compatibility` decorator provides runtime version gating |
| `dellemc.powermax` | `PyU4V >=10.2.0.3,==10.2.0.*` | Static import | Range-pinned; both floor and ceiling defined |
| `dellemc.unity` | `storops>=1.2.12` | Static import | Floor-only pin |
| `dellemc.openmanage` | `omsdk`, `netaddr>=0.7.19` | Static import | Cross-collection deps on `ansible.utils`, `ansible.windows` |

### Ansible Version Requirements

| Collection | `requires_ansible` |
|---|---|
| `dellemc.powerscale` | `>=2.15.0` |
| `dellemc.openmanage` | Per `galaxy.yml` deps on `ansible.utils >=2.10.2`, `ansible.windows >=1.14.0` |

---

## Known Constraints

1. **isilon-sdk is loaded dynamically** — `dellemc.powerscale` imports `isilon_sdk` at runtime via `importlib`. Static analysis tools (linters, dependency scanners) will not detect it. The SDK is declared only in `requirements.txt`. Agents adding imports must not assume static import is feasible for this SDK.

2. **SDK version coupling is strict** — Each collection release is tested against exactly one SDK version (or a tight range for PowerMax). A mismatch between the collection and SDK version is a blocking defect, not a warning. Never update `requirements.txt` SDK versions without verifying against the corresponding collection release notes.

3. **`shared_library/` and `libraries/` are the same pattern** — The naming difference between `ansible-powerscale` (`shared_library/`) and `ansible-powerstore`/`ansible-powerflex` (`libraries/`) is a historical convention, not a structural distinction. Both serve as the base class + domain helper layer above `utils.py`.

4. **PowerMax and Unity have no base class** — These two collections do not have a `libraries/` or `shared_library/` directory. Module classes call `utils.get_<platform>_connection()` directly in their own `__init__`. There is no `<Platform>Base` to subclass.

5. **`meta/runtime.yml` is the source of truth for action groups** — The `dellemc.<platform>.all` action group is defined here. Every new module added to a collection MUST be appended to this list or `module_defaults` with the group will silently skip it.

6. **Tombstone entries in `runtime.yml` are permanent** — Deprecated `dellemc_<platform>_*` prefixed module names have tombstone entries. These must not be removed; they are the backward-compatibility contract for playbooks written before the FQCN rename.

7. **`verify_ssl: false` is a lab-only setting** — All modules accept `verify_ssl`/`validate_certs`. Setting it to `false` in production violates the security constitution. Modules must not default to skipping verification.

8. **OpenManage does not follow the storage module layout** — Agents working on `dellemc.openmanage` must not apply the `plugins/module_utils/storage/dell/` path, base class, or `shared_library/` patterns. That collection has its own flat `module_utils/` layout with per-API-surface clients.

9. **Example playbooks are mandatory** — Every new or modified module must ship a working example playbook in `playbooks/modules/`. Syntax check (`ansible-playbook --syntax-check`) must pass. This is a P0 delivery item.

---

## Change History

| Date | Feature | What Changed | Author |
|------|---------|-------------|--------|
| 2026-06-04 | Initial architecture | First capture of providers/ workspace structure and storage collection internal pattern | architecture-agent |
