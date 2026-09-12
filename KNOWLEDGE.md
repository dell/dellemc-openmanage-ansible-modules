# KNOWLEDGE.md — dellemc-openmanage-ansible-modules

<!-- yaml-metadata-start -->
scope_paths: ["./"]
capture_git_sha: "ee9af199b7731b8a1dda4970d606e145f287fb29"
status: "current"
auto_update: false
preview_before_apply: true
scaffold_version: "1.0"
# session_state: { is_complete: true }
<!-- yaml-metadata-end -->

<!-- quick-reference-start -->
## Agent Quick Reference

| Section | Heading | Summary | never_again_count |
|---------|---------|---------|-------------------|
| Component Overview | `## Component Overview` | dellemc.openmanage collection for OpenManage Enterprise / iDRAC / OMEVV | — |
| Architectural Rationale | `## Architectural Rationale` | omsdk, netaddr SDK; Ansible collection pattern | — |
| Failure Modes & Gotchas | `## Failure Modes & Gotchas` | SDK coupling, idempotency, verify_ssl | 0 |
| Implicit Contracts | `## Implicit Contracts` | Connection params, ordering, action groups | — |
<!-- quick-reference-end -->

## Five Questions Quick Reference

### What does it do?
Ansible Galaxy collection `dellemc.openmanage` (v10.0.2). Provides 105 modules and 16 roles for declarative, idempotent management of Dell PowerEdge server lifecycle management via OpenManage Enterprise, iDRAC Redfish, and OMEVV. Uses `omsdk, netaddr` (netaddr>=0.7.19) Python SDK.

### How do you modify it?
Create module file in `plugins/modules/`, add example playbook in `playbooks/modules/`, add unit test in `tests/unit/plugins/modules/`, append module FQCN to `meta/runtime.yml` action group.

### What breaks?
SDK version mismatch is a blocking defect. Missing tombstone/redirect entry leaves deprecated module names unresolved. `validate_certs: false` in production violates security constitution.

### What depends on it?
`omsdk, netaddr` netaddr>=0.7.19, Ansible >= 2.15.0. Ordering: dependent resources must exist before referencing them.

### What's undocumented?
Flat `module_utils/` layout with per-API-surface clients: `ome.py`, `idrac_redfish.py`, `redfish.py`, `rest_api.py`, `omevv.py`, `session_utils.py`, `dellemc_idrac.py`. Standard Ansible logging — no custom file handler.

---

## Component Overview

Ansible Galaxy collection `dellemc.openmanage` (v10.0.2) for Dell PowerEdge server lifecycle management via OpenManage Enterprise, iDRAC Redfish, and OMEVV. 105 modules and 16 roles covering firmware updates, baselines, templates, configuration compliance, device discovery, user management, BIOS settings, boot order, certificates, LDAP, SCP import/export, virtual media, power management, storage configuration, network settings, and more.

---

## Architectural Rationale

Standard Ansible Galaxy collection layout. Each module is a self-contained Python file under `plugins/modules/` that communicates with the OpenManage Enterprise / iDRAC / OMEVV REST API through the `omsdk, netaddr` SDK.

**SDK strategy:** Static import. Version pinned at `netaddr>=0.7.19` in `requirements.txt`.


### Evolution

Early collections used a flat module structure with duplicated auth
and API logic in each module. The shared base class was introduced
after initial module growth to centralize authentication, argument
parsing, and API client initialization. Major refactors include:

- Base class introduction (centralized SDK initialization)
- Module naming standardization
- SDK / REST client improvements
- Improved error handling consistency

---

## Failure Modes & Gotchas

### 1. SDK version coupling

Each collection release is tested against exactly one SDK version (or tight range for PyU4V). A mismatch between collection and SDK version is a blocking defect. Never update `requirements.txt` SDK versions without verifying against the corresponding collection release notes.

### 2. Idempotency assumptions

Modules are designed to be idempotent but some parameters may be accepted by the module yet ignored by the underlying API. Always verify with a second run.

### 3. Verify SSL setting

`validate_certs: false` is used in example playbooks but is a lab-only setting. Production requires `true`. Modules must not default to skipping verification.

### 4. Acceptance test cleanup

If tests fail mid-run, resources may be left on the array. Clean up manually before re-running.

### Structurally Distinct Layout

This collection does **not** follow the storage collection layout. Key differences:
- `module_utils/` is flat (no `storage/dell/` path)
- Per-API-surface clients (`ome.py`, `idrac_redfish.py`, `redfish.py`, `omevv.py`)
- 35 iDRAC-specific utility helpers in `module_utils/idrac_utils/`
- 3 OMEVV-specific utility helpers in `module_utils/omevv_utils/`
- 9 doc fragments (vs 1 per storage collection)
- 16 Ansible roles for iDRAC and Redfish operations
- `bindep.txt` for system package requirements (no storage equivalent)
- Cross-collection dependencies: `ansible.utils`, `ansible.windows`
- 1 inventory plugin (`ome_inventory`)

### Multiple API Surfaces

Modules target three distinct APIs:
- **OME** — OpenManage Enterprise REST API (fleet management)
- **iDRAC** — Direct iDRAC Redfish API (server management)
- **OMEVV** — OpenManage Enterprise VMware integration


### 5. Idempotency drift

Occasional idempotency failures where a module reports `changed=false`
but state actually changed on the array. Caused by incomplete state
comparison logic — some parameters accepted by the module are ignored
by the underlying API. Always verify with a second run.

### 6. SDK import failures

Dependency or version mismatches between the collection and its SDK
cause import failures at module load time. Manifests as
`ModuleNotFoundError` or `ImportError` with no actionable message
unless `-vvv` is used.

### 7. Check mode inaccuracies

Not all modules fully simulate changes correctly in check mode.
Some modules report `changed=true` in check mode but would actually
make no change, or vice versa. Treat check mode as advisory, not
authoritative.

### Never Again

#### NA-001: SDK version mismatch causing silent failures
- **Impact:** Modules loaded but returned incorrect data due to
  SDK API changes between versions.
- **Constraint:** SDK version must be pinned exactly in
  `requirements.txt`. Never update without full test pass.
- **Applies to:** All Dell Ansible collections.

#### NA-002: Idempotency regression on update operations
- **Impact:** Repeated playbook runs made unintended changes to
  array resources due to incomplete state comparison.
- **Constraint:** Every module must compare full current state
  before applying changes.
- **Applies to:** All Dell Ansible collections.

#### NA-003: Orphaned resources from test failures
- **Impact:** Test resources left on array after test failure,
  consuming capacity.
- **Constraint:** Manual cleanup required after failed test runs.
- **Applies to:** All Dell Ansible collections.
### Evolution

Failure modes evolved with the base class introduction. Error
handling was standardized across modules during the naming
convention refactor. SDK import failures became less common after
the `HAS_*` flag pattern was adopted consistently.

---

## Performance Characteristics

**Sequential execution:** Ansible executes modules sequentially per
host within a play. Large inventories with many tasks experience
linear performance degradation. No built-in batching or pipelining
at the module level.

**API rate limiting:** OpenManage/iDRAC arrays enforce implicit
throttling under heavy parallel execution (high Ansible fork count).
Reduce `forks` or add `throttle` to tasks hitting the same array.

**Bulk operations:** Module execution is slower for bulk operations
due to per-task API calls with no batching support. Async operations
(where supported) can mitigate but add complexity.

**No connection reuse:** Each module invocation creates a new SDK
client and HTTP session. No connection pooling across tasks.

### Evolution

Performance improved after the base class centralized SDK
initialization, reducing per-module overhead. Connection reuse
remains an open area for improvement.

---

## Implicit Contracts

**Connection parameters required:** All modules require `hostname`, `username`, `password`, `validate_certs` — these are not optional.

**Resource ordering:** Dependent resources must exist before being referenced (e.g., filesystem before snapshot, volume group before volumes, policies before assignment).

**Runtime registration:** Deprecated module names must have tombstone or redirect entries in `meta/runtime.yml`.

### Evolution

Connection parameter patterns were established early and carried
forward. Resource ordering constraints are implicit — the API
returns errors but the collection does not enforce ordering.

---

## Threading & Synchronization

Ansible handles concurrency via forks at the play level. Individual
module executions are single-threaded. However, multiple forks
hitting the same OpenManage/iDRAC array simultaneously causes:

**API contention:** High fork counts cause throttling or transient
errors from the array API. Mitigate with `throttle: N` on tasks
targeting the same array.

**Connection pool exhaustion:** Possible when many forks execute
without HTTP session reuse. Each fork creates independent SDK
client connections.

**Race conditions on shared resources:** Concurrent modifications
to interdependent resources (e.g., volume + host mapping,
replication configurations) can produce inconsistent state.
Serialize dependent operations with `serial: 1` or task ordering.

### Evolution

Concurrency issues became more visible as collections grew and
users ran larger playbooks with higher fork counts against single
arrays.

---

## Build System & Configuration

| Command | Description |
|---------|-------------|
| `ansible-galaxy collection build` | Build collection tarball |
| `ansible-galaxy collection install <tarball>` | Install locally |
| `pytest tests/unit/` | Run unit tests |
| `ansible-playbook --syntax-check` | Validate playbook syntax |

---

## Operational Knowledge

**Logging:** Enable `-vvv` for detailed output including API
request/response payloads. Correlate Ansible output with array
logs for full troubleshooting.

**Common support scenarios:**
- Authentication failures — verify `hostname`, credentials,
  and `validate_certs` settings
- Idempotency issues — run playbook twice, compare `changed`
  status
- Timeout / async completion problems — increase timeout
  parameters, check array load

**Test environment requirements:**
- Dedicated OpenManage/iDRAC array or simulator
- Stable API version matching SDK pin
- Isolated test datasets (avoid shared resources)

### Evolution

Debugging patterns improved with `-vvv` adoption as standard
practice. Common failure patterns documented after recurring
support cases.

---

## General Context

No additional context beyond what has been captured.

### Open Issues

No TODO/FIXME/HACK markers found in non-test source files.

---

## References

- [Ansible Galaxy — dellemc.openmanage](https://galaxy.ansible.com/dellemc/openmanage)
- [Ansible Collection Developer Guide](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html)

---

## Governance Spec Discrepancies

No discrepancies detected.
