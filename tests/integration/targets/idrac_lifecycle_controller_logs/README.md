# iDRAC Lifecycle Controller Logs Integration Tests

This directory contains integration tests for the `dellemc.openmanage.idrac_lifecycle_controller_logs` Ansible module.

## Test Coverage

### Firmware & Service Checks (4 tests)
- `firmware_version_meets_minimum.yaml` - Verify minimum firmware version requirement
- `firmware_version_below_minimum.yaml` - Verify firmware version validation
- `lc_log_service_enabled.yaml` - Verify LC log service is enabled
- `lc_log_service_disabled.yaml` - Verify handling of disabled LC log service

### Log Retrieval & Filtering (6 tests)
- `full_retrieval_without_filters.yaml` - Retrieve all LC logs
- `date_range_bounded_retrieval.yaml` - Date-range-bounded retrieval
- `filter_by_severity.yaml` - Filter logs by severity level
- `filter_by_category.yaml` - Filter logs by category
- `combined_filters.yaml` - Apply multiple filters simultaneously
- `invalid_date_range.yaml` - Validate date range validation
- `filters_produce_no_results.yaml` - Handle empty result sets

### Metadata Query (1 test)
- `metadata_query.yaml` - Query LC log metadata

### Export Functionality (4 tests)
- `export_json.yaml` - Export logs in JSON format
- `export_csv.yaml` - Export logs in CSV format
- `export_text.yaml` - Export logs in text format
- `insufficient_write_permissions.yaml` - Validate permission checks

### Log Clear Operations (4 tests)
- `clear_logs_with_confirmation.yaml` - Clear logs with explicit confirmation
- `clear_logs_without_confirmation.yaml` - Verify confirmation requirement
- `clear_timeout.yaml` - Handle clear operation timeouts
- `clear_export_abort.yaml` - Abort clear if export fails

### Comment Insertion (3 tests)
- `insert_comment.yaml` - Insert comment into log entry
- `comment_exceeds_256_chars.yaml` - Validate comment length limit
- `comment_insufficient_privilege.yaml` - Validate comment insertion permissions

### Storage Management (3 tests)
- `storage_warning_triggered.yaml` - Detect storage utilization warnings
- `storage_below_threshold.yaml` - Verify no warning when below threshold
- `log_rotation.yaml` - Verify automated log rotation

### MessageRegistry (2 tests)
- `message_registry_available.yaml` - Enrich logs with MessageRegistry data
- `message_registry_unavailable.yaml` - Graceful fallback when registry unavailable

## Running Tests

### Run all tests
```bash
ansible-test integration idrac_lifecycle_controller_logs -v
```

### Run specific test
```bash
ansible-test integration idrac_lifecycle_controller_logs --tags firmware_version_meets_minimum -v
```

### Run tests by category
```bash
# Firmware tests
ansible-test integration idrac_lifecycle_controller_logs --tags "firmware_version_meets_minimum,firmware_version_below_minimum" -v

# Filter tests
ansible-test integration idrac_lifecycle_controller_logs --tags "filter_by_severity,filter_by_category,combined_filters" -v

# Export tests
ansible-test integration idrac_lifecycle_controller_logs --tags "export_json,export_csv,export_text" -v
```

## Test Prerequisites

- iDRAC with LC log service enabled
- Valid iDRAC credentials (set via environment variables or inventory)
- Ansible >= 2.14
- Python >= 3.9

## Environment Variables

Override default iDRAC connection parameters:
```bash
export IDRAC_HOST="192.168.1.100"
export IDRAC_USERNAME="admin"
export IDRAC_PASSWORD="password"
ansible-test integration idrac_lifecycle_controller_logs -v
```

## Test Data

Default test variables are defined in `defaults/main.yml`:
- iDRAC connection parameters
- Filter values (severity, category, date ranges)
- Export paths
- Comment test data
- Storage thresholds
