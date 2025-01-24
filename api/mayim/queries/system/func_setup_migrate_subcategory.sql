CREATE OR REPLACE FUNCTION migrate_subcategory(
    replacement_id UUID,
    original_id UUID,
    param_user_id UUID
) RETURNS VOID AS $$
BEGIN
    -- Insert a system message for each ticket indicating the Category change
    INSERT INTO messages (type, ticket_id, author_id, content)
    SELECT
        'SYSTEM'::MessageType,
        t.id,
        param_user_id,
        'SYSTEM: SubCategory Migration'
    FROM Tickets t
    WHERE subcategory_id = original_id;

    -- Update the Category ID of each ticket
    UPDATE tickets
    SET subcategory_id = replacement_id
    WHERE subcategory_id = original_id;

    -- Delete the original SubCategory
    DELETE FROM subcategories
    WHERE id = original_id;
END;
$$ LANGUAGE plpgsql;
