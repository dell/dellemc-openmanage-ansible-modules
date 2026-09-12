# AGENTS.md - Dell OpenManage Ansible Modules

## Project Overview

This is the Ansible Galaxy collection for Dell OpenManage Enterprise (OME) and iDRAC server management. It provides Ansible modules, roles, and inventory plugins for automating Dell server fleet management, firmware updates, configuration, and monitoring.

- **Language:** Python
- **Collection namespace:** `dellemc.openmanage`
- **Collection version:** 10.0.2
- **SDK:** `omsdk` (OpenManage SDK) + `netaddr`
- **License:** GNU General Public License v3.0

## Architecture

The collection follows the standard Ansible Galaxy collection layout. Modules communicate with Dell server management interfaces:
- **OME modules** — Talk to OpenManage Enterprise REST API for fleet-level operations.
- **iDRAC modules** — Talk to iDRAC Redfish API for individual server management.
- **Inventory plugins** — Discover and inventory Dell servers from OME.

### Authentication

- **OME modules:** `hostname`, `username`, `password`, `port`, `validate_certs`.
- **iDRAC modules:** `idrac_ip`, `idrac_user`, `idrac_password`, `idrac_port`, `validate_certs`.

### SDK Strategy

Uses `omsdk` — the Dell OpenManage SDK — plus `netaddr` for network utilities. Both are installed via `pip` and pinned in `requirements.txt`.

### Module, Role, and Plugin Count

The collection includes approximately 213 modules, 16 roles, and inventory plugins covering OME templates, firmware baselines, server profiles, discovery, deployment, iDRAC BIOS/network/storage/user configuration, firmware updates, diagnostics, certificates, and OMEVV (vCenter integration).

## Directory Structure

```
galaxy.yml                        Collection metadata (namespace, name, version)
plugins/
  modules/                        Ansible modules (one .py file per resource/action)
  module_utils/                   Shared utility classes
    idrac_utils/                  iDRAC-specific utilities
    omevv_utils/                  OMEVV (vCenter) utilities
  doc_fragments/                  Shared documentation fragments
  inventory/                      Dynamic inventory plugins
meta/                             Collection metadata (runtime.yml)
roles/                            Ansible roles (16 roles for deployment/config workflows)
tests/
  unit/
    plugins/                      Unit tests (pytest)
  integration/
    targets/                      Integration test targets
playbooks/                        Example playbooks
docs/                             Module documentation
changelogs/                       Release changelog fragments
requirements.txt                  Python dependencies (omsdk, netaddr)
requirements.yml                  Ansible collection dependencies
Makefile                          Build and test targets
```

## Build Commands

| Command | Description |
|---------|-------------|
| `ansible-galaxy collection build` | Build the collection tarball |
| `ansible-galaxy collection install <tarball>` | Install the collection locally |
| `pytest tests/unit/` | Run unit tests |
| `make` | Build targets (see Makefile) |

## Testing

### Unit Tests

- Test files follow `test_*.py` convention in `tests/unit/plugins/`.
- Framework: `pytest` with `unittest.mock` for mocking.
- Configuration in `pytest.ini`.
- No hardware required.

### Integration Tests

- Integration tests in `tests/integration/targets/`.
- **Requires live OME/iDRAC hardware.**

### Running Tests

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r test-requirements.txt

# Run unit tests
pytest tests/unit/ -v
```

## Code Style and Conventions

### Module Pattern

Each module follows the standard Ansible module pattern:
1. `DOCUMENTATION`, `EXAMPLES`, and `RETURN` docstrings at the top.
2. An `AnsibleModule` argument spec defining parameters.
3. A main class that wraps API calls and handles idempotency.
4. `module.exit_json()` for success, `module.fail_json()` for errors.

### Shared Utilities

- `plugins/module_utils/` contains shared base classes, HTTP helpers, and SDK wrappers.
- `plugins/module_utils/idrac_utils/` — iDRAC Redfish-specific helpers.
- `plugins/module_utils/omevv_utils/` — OMEVV (vCenter integration) helpers.
- `plugins/doc_fragments/` — Reusable documentation fragments for OME and iDRAC connection parameters.

### Roles

Roles in `roles/` provide end-to-end workflows such as server deployment, firmware updates, iDRAC configuration, and OME template management.

### File Header

All source files must include the Dell copyright and GPL v3.0 license header.

## Common Development Tasks

### Adding a New Module

1. Create `plugins/modules/<resource>.py` following the Ansible module pattern.
2. Add shared utilities in `plugins/module_utils/` if needed.
3. Add documentation fragments in `plugins/doc_fragments/` for new connection params.
4. Add unit tests in `tests/unit/plugins/`.
5. Add example playbooks in `playbooks/`.
6. Update `changelogs/` with a changelog fragment.

### Adding a New Role

1. Create `roles/<role_name>/` with `tasks/`, `defaults/`, `meta/`, and `templates/`.
2. Document in `roles/<role_name>/README.md`.

## CI/CD

GitHub Actions workflows in `.github/workflows/`. Code coverage tracked via `codecov.yml`.

## Code Ownership

All files are owned by the maintainers defined in `.github/CODEOWNERS`.
