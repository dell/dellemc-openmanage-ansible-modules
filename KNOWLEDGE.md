# KNOWLEDGE.md — dellemc-openmanage-ansible-modules

<!-- yaml-metadata-start -->
scope_paths: ["./"]
capture_git_sha: "b3b50fb947ab41286f235020b65caf5e1179c8d0"
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
SDK version mismatch is a blocking defect. Missing action group entry causes `module_defaults` to silently skip the module. `validate_certs: false` in production violates security constitution.

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

### Never Again

No incident-derived constraints recorded.

---

## Performance Characteristics

TBD — requires SME input.

---

## Implicit Contracts

**Connection parameters required:** All modules require `hostname`, `username`, `password`, `validate_certs` — these are not optional.

**Resource ordering:** Dependent resources must exist before being referenced (e.g., filesystem before snapshot, volume group before volumes, policies before assignment).

**Action group registration:** Every new module must be appended to the `dellemc.openmanage.all` action group in `meta/runtime.yml`.

---

## Threading & Synchronization

Ansible handles concurrency via forks at the play level. Individual module executions are single-threaded.

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

Standard Ansible logging — no custom file handler.

---

## General Context

No additional context beyond what has been captured.

---

## References

- [Ansible Galaxy — dellemc.openmanage](https://galaxy.ansible.com/dellemc/openmanage)
- [Ansible Collection Developer Guide](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html)

---

## Governance Spec Discrepancies

No discrepancies detected.
