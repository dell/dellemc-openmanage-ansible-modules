# iDRAC Lifecycle Controller Logs Integration Tests

This directory contains integration tests for the `idrac_lifecycle_controller_logs` Ansible module.

## Test Structure

- `tests/` - Contains individual test playbooks for different scenarios
- `defaults/` - Default variables for the test suite
- `tasks/` - Common tasks used across tests
- `files/` - Test data files

## Running Tests

To run all tests:
```bash
ansible-test integration idrac_lifecycle_controller_logs -v
```

To run a specific test:
```bash
ansible-test integration idrac_lifecycle_controller_logs --tags firmware_version_meets_minimum -v
```

## Test Categories

### Firmware & Service Checks
- `firmware_version_meets_minimum.yaml` - Verify minimum firmware version requirement
- `firmware_version_below_minimum.yaml` - Verify firmware version validation
- `lc_log_service_enabled.yaml` - Verify LC log service is enabled
- `lc_log_service_disabled.yaml` - Verify handling of disabled LC log service

### Log Retrieval & Filtering
- `full_retrieval_without_filters.yaml` - Retrieve all LC logs
- `filter_by_severity.yaml` - Filter logs by severity level
- `filter_by_category.yaml` - Filter logs by category
- `combined_filters.yaml` - Apply multiple filters simultaneously
- `invalid_date_range.yaml` - Validate date range validation
- `filters_produce_no_results.yaml` - Handle empty result sets

### Log Export
- `export_json.yaml` - Export logs in JSON format
- `export_csv.yaml` - Export logs in CSV format
- `export_text.yaml` - Export logs in text format
- `insufficient_write_permissions.yaml` - Validate permission checks

### Log Management
- `clear_logs_with_confirmation.yaml` - Clear logs with explicit confirmation
- `clear_logs_without_confirmation.yaml` - Clear logs without confirmation
- `clear_timeout.yaml` - Handle clear operation timeouts
- `clear_export_abort.yaml` - Abort clear if export fails

### Comments & Metadata
- `insert_comment.yaml` - Insert comment into log entry
- `comment_exceeds_256_chars.yaml` - Validate comment length limit
- `comment_insufficient_privilege.yaml` - Validate comment insertion permissions
- `metadata_query.yaml` - Query LC log metadata

### Storage Management
- `storage_warning_triggered.yaml` - Detect storage utilization warnings
- `storage_below_threshold.yaml` - Verify no warning when below threshold
- `log_rotation.yaml` - Verify automated log rotation

### MessageRegistry
- `message_registry_available.yaml` - Enrich logs with MessageRegistry data
- `message_registry_unavailable.yaml` - Graceful fallback when registry unavailable
