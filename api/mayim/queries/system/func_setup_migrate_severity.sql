CREATE OR REPLACE FUNCTION migrate_severity(
    replacement_id UUID,
    original_id UUID,
    param_user_id UUID
) RETURNS VOID AS $$
BEGIN
    -- Insert a system message for each ticket indicating the Severity change
    INSERT INTO messages (type, ticket_id, author_id, content)
    SELECT
        'SYSTEM'::MessageType,
        t.id,
        param_user_id,
        'SYSTEM: Severity Migration'
    FROM Tickets t
    WHERE severity_id = original_id;

    -- Update the Severity ID of each ticket
    UPDATE tickets
    SET severity_id = replacement_id
    WHERE severity_id = original_id;

    -- Update the default Severity in the config table if it matches the original SLA
    IF EXISTS (
        SELECT 1
        FROM config
        WHERE original_id = (
            SELECT default_severity
            FROM config
            ORDER BY created_at DESC
            LIMIT 1
        )
    ) THEN
        INSERT INTO config (
            default_sla,
            default_severity,
            default_assignee
        )
        VALUES (
            (
                SELECT default_sla
                FROM config
                ORDER BY created_at DESC
                LIMIT 1
            ),
            replacement_id,
            (
                SELECT default_assignee
                FROM config
                ORDER BY created_at DESC
                LIMIT 1
            )
        );
    END IF;

    -- Delete the original SLA
    DELETE FROM severity
    WHERE id = original_id;
END;
$$ LANGUAGE plpgsql;
