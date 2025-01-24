-- Use Migrate Subcategory
SELECT migrate_subcategory(
    replacement_id => $replacement_id,
    original_id => $original_id,
    param_user_id => $user_id
)
