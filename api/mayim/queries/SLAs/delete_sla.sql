-- Use Migrate_SLA function
SELECT migrate_sla(
    replacement_id => $replacement_id,
    original_id => $original_id,
    param_user_id => $user_id
);
