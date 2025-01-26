-- Use Migrate Category function
SELECT migrate_category(
    replacement_id => $replacement_id,
    original_id => $original_id,
    param_user_id => $user_id
);
