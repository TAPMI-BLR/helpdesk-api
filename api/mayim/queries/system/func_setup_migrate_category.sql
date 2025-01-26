CREATE OR REPLACE FUNCTION migrate_category(
    replacement_id UUID,
    original_id UUID,
    param_user_id UUID
) RETURNS VOID AS $$
BEGIN
    -- Update Parent ID of all subcategories to the replacement ID
    UPDATE subcategories
    SET parent_id = replacement_id
    WHERE parent_id = original_id;

    -- Delete the original Category
    DELETE FROM categories
    WHERE id = original_id;
END;
$$ LANGUAGE plpgsql;
