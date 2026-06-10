# KNOWLEDGE.md — providers/

<!-- Filename: Use KNOWLEDGE.md for single-component directories.
     Use KNOWLEDGE-<component>.md when a directory covers multiple components.
     See governance/constitutions/appendices/knowledge-loading.md Section 0. -->

<!-- yaml-metadata-start -->
scope_paths: ["./"]
capture_git_sha: "50215ac9190c7f50bd14327ee114f8dd2ef88e5c"
status: "current"
auto_update: false
preview_before_apply: true
scaffold_version: "1.0"
# session_state: { is_complete: true }
<!-- yaml-metadata-end -->

<!-- quick-reference-start -->
## Agent Quick Reference

> Machine-readable navigation aid for agents performing section-level selective loading.
> Section locators are heading strings only — no line numbers.
> never_again_count: N means N production-incident-derived constraints exist in Failure Modes.

| Section | Heading | Summary | never_again_count |
|---------|---------|---------|-------------------|
| Component Overview | `## Component Overview` | High-level purpose and boundaries | — |
| Architectural Rationale | `## Architectural Rationale` | Why built this way; key tradeoffs | — |
| Failure Modes & Gotchas | `## Failure Modes & Gotchas` | Production incidents; Never Again constraints | 0 |
| Performance Characteristics | `## Performance Characteristics` | Throughput; latency; resource limits | — |
| Implicit Contracts | `## Implicit Contracts` | Undocumented assumptions; caller invariants | — |
| Threading & Synchronization | `## Threading & Synchronization` | Thread safety; lock ordering; async patterns | — |
<!-- quick-reference-end -->

## Five Questions Quick Reference

### What does it do?
`providers/` is a workspace containing 6 Ansible Galaxy collections published under the `dellemc` namespace. Each delivers declarative, idempotent resource management for a specific Dell hardware platform. Five collections target storage arrays (PowerScale 56 modules, PowerStore 45, PowerFlex 22, PowerMax 17, Unity 18) and share a canonical internal layout. OpenManage (105 modules + 16 roles) targets PowerEdge server lifecycle management with a structurally distinct layout developed by a different team.

### How do you modify it?
To add a new module to a storage collection: create the module file in `plugins/modules/`, add corresponding example playbook in `playbooks/modules/`, add unit test in `tests/unit/plugins/modules/`, and append the module FQCN to `meta/runtime.yml` under the `dellemc.<platform>.all` action group. For OpenManage, the module_utils layout is flat (no `storage/dell/` path) and includes roles in addition to modules.

### What breaks?
No known production incidents. Possible silent-failure constraints: partial parameter acceptance (ignored fields), idempotency mismatch, async operations treated as completed, duplicate resource scenarios, capacity/pool constraints not surfaced clearly, initiator/host configuration inconsistencies, and version drift between collection and array firmware.

### What depends on it?
Ordering requirements: filesystem must exist before snapshot; volume group must exist before creating volumes in it; protection/performance policies must exist before assignment. All modules require connection parameters (host, user, password, verify_ssl) — not optional. `verify_ssl: false` is lab-only; production requires `true`.

### What's undocumented?
- **isilon-sdk dynamic import:** `dellemc.powerscale` imports `isilon_sdk` at runtime via `importlib.import_module()` to handle version-specific package names. Static analysis tools will not detect this dependency. [source: code-analysis, file: ansible-powerscale/plugins/module_utils/storage/dell/utils.py:273]
- **PowerMax TODO markers:** `ansible-powermax/plugins/modules/volume.py` contains 3 TODO comments about PyU4V implementation gaps (lines 466, 523, 567). [source: code-analysis]
- **PowerFlex version gating:** `@powerflex_compatibility` decorator provides runtime version checking for module compatibility with PowerFlex API versions. [source: code-analysis, file: ansible-powerflex/plugins/module_utils/storage/dell/libraries/powerflex_base.py:121]
- **Logging deviation:** PowerScale, PowerFlex, PowerMax, Unity write `ansible_<platform>.log` to working directory by default. PowerStore defaults to NullHandler (no file logging) — enable via env toggle (`1`/`true`/`yes`). [source: code-analysis, file: ansible-powerstore/plugins/module_utils/storage/dell/utils.py:177-183]

---

## Component Overview

`providers/` is a workspace containing 6 independent Git repos, each an Ansible Galaxy collection published under the `dellemc` namespace. The workspace structure is:

- `ansible-powerscale/` — 56 modules for PowerScale storage arrays, SDK `isilon-sdk==0.6.0` (dynamically imported)
- `ansible-powerstore/` — 45 modules for PowerStore storage arrays, SDK `PyPowerStore==3.4.2`
- `ansible-powerflex/` — 22 modules for PowerFlex storage arrays, SDK `PyPowerFlex==2.0.0`
- `ansible-powermax/` — 17 modules for PowerMax storage arrays, SDK `PyU4V >=10.2.0.3,==10.2.0.*`
- `ansible-unity/` — 18 modules for Unity storage arrays, SDK `storops>=1.2.12`
- `dellemc-openmanage-ansible-modules/` — 105 modules + 16 roles for PowerEdge server lifecycle management, SDKs `omsdk` and `netaddr>=0.7.19`

All five storage collections share a canonical layout: `plugins/modules/` (one file per resource), `plugins/module_utils/storage/dell/` (utils.py + optional libraries/), `playbooks/modules/` (example playbooks), `tests/unit/` (unit tests), `meta/runtime.yml` (action groups and tombstones), and `galaxy.yml` (collection metadata). OpenManage deviates with a flat `module_utils/` layout, per-API-surface clients, and roles.

---

## Architectural Rationale

All Dell providers are architected mostly the same way. The five storage collections share a canonical layout to maintain consistency across the storage product line. OpenManage has a structurally distinct layout because it was developed by a different team and architect. SDK versioning differs by team — PowerMax uses a range-pinned version while others are single-version pinned. The `providers/` workspace exists as a local grouping so that the same knowledge can be built for all collections as generic information.

The reason for PowerScale's dynamic import of `isilon-sdk` is uncertain — SME input required.

### Evolution

Phase 0 scan could not determine evolution from code analysis. SME input required for how and why the architecture changed over time.

---

## Failure Modes & Gotchas

No known production failure modes or edge cases identified by the SME. Common mistakes fall into categories: authentication, idempotency assumptions, API behavior, module usage, and environment setup.

Possible constraints that may cause silent failures if violated:
- **Partial Parameter Acceptance (Ignored Fields):** Some parameters may be accepted by the module but ignored by the underlying API
- **Idempotency Mismatch:** Modules may not be truly idempotent in all scenarios despite the framework's idempotency design
- **Async Operations Treated as Completed:** Long-running operations may be reported as completed before they actually finish
- **Duplicate Resource Scenarios:** Behavior when creating resources that already exist may be inconsistent
- **Capacity / Pool Constraints Not Surfaced Clearly:** Storage capacity or pool limitations may not be surfaced as clear error messages
- **Initiator / Host Configuration Inconsistencies:** Host or initiator configuration may have platform-specific inconsistencies
- **Version Drift Between Collection and Array Firmware:** Collection and array firmware version mismatches may cause unexpected behavior

### Never Again

No incident-derived constraints recorded. If you know of past incidents affecting this component, please record them during the next Knowledge Extraction session.

### Evolution

Phase 0 scan could not determine evolution from code analysis. SME input required for how failure modes have changed.

---

## Performance Characteristics

Phase 0 scan could not determine performance characteristics from code analysis. SME input required for bottlenecks, scaling limits, tuning parameters, benchmarks, and known performance cliffs.

### Evolution

Phase 0 scan could not determine evolution from code analysis. SME input required for how performance characteristics changed.

---

## Implicit Contracts

**Ordering requirements:**
- Filesystem must be created before snapshot (PowerScale example playbook creates filesystem at line 40-56, then snapshot at line 58-70)
- Volume group must exist before creating volumes in it (PowerStore example playbook references `vg_name` at line 39)
- Protection policies and performance policies referenced by name must exist before being assigned to volumes

**Connection parameters:**
- All modules require connection parameters (`onefs_host`/`array_ip`/`hostname`, `api_user`/`username`, `api_password`/`password`, `verify_ssl`/`validate_certs`) — these are not optional
- `verify_ssl: false` is used in example playbooks but is a lab-only setting; production requires `true`

**Environment configuration:**
- PowerStore supports an environment variable toggle for file logging (via `os.getenv` in utils.py) — truthy values ("1", "true", "yes") enable file logging

### Evolution

Phase 0 scan could not determine evolution from code analysis. SME input required for how implicit contracts changed.

---

## Threading & Synchronization

Phase 0 scan could not determine threading and synchronization patterns from code analysis. SME input required for concurrency model, lock ordering, callback threading, and thread safety guarantees.

### Evolution

Phase 0 scan could not determine evolution from code analysis. SME input required for how the concurrency model changed.

---

## Build System & Configuration

Phase 0 scan could not determine build system and configuration from code analysis. SME input required for non-obvious build dependencies, conditional compilation flags, platform-specific build paths, and configuration that affects runtime behavior.

### Evolution

Phase 0 scan could not determine evolution from code analysis. SME input required for how build and configuration changed.

---

## Operational Knowledge

**Logging behavior — deviation between collections (code-verified):**
- **PowerScale, PowerFlex, PowerMax, Unity:** `get_logger()` uses `logging.basicConfig(filename=...)` plus a `CustomRotatingFileHandler` and writes a log file **by default** to the working directory: `ansible_powerscale.log`, `ansible_powerflex.log`, `ansible_powermax.log`, `ansible_unity.log` respectively. Rotation: 5 MB max, 5 backups.
- **PowerStore (outlier):** `get_logger()` defaults to a `NullHandler` — **no file is written by default**. File logging is enabled only via an explicit flag or the environment-variable toggle (truthy values `1`/`true`/`yes`). Failures to initialize the file handler are caught and the module continues without logging (fail-safe). [file: ansible-powerstore/plugins/module_utils/storage/dell/utils.py:133-203]

For debugging connection or operation failures: on the four collections with default file logging, inspect the `ansible_<platform>.log` file in the playbook's working directory. On PowerStore, enable logging first via the env toggle before reproducing.

Phase 0 scan could not determine deployment runbooks, monitoring integrations, or common support scenarios from code analysis. SME input required.

### Evolution

Phase 0 scan could not determine evolution from code analysis. SME input required for how operational knowledge changed.

---

## General Context

No additional team context, ownership, historical background, cross-cutting concerns, or other important information beyond what has been captured.

---

## References

No external references captured.

---

## Governance Spec Discrepancies

No discrepancies detected between code/SME knowledge and loaded governance specs.
