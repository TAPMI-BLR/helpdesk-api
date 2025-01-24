-- Use Migrate Severity function
SELECT migrate_severity(
    replacement_id => $replacement_id,
    original_id => $original_id,
    param_user_id => $user_id
);
