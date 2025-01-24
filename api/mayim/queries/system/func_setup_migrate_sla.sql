CREATE OR REPLACE FUNCTION migrate_sla(
    replacement_id UUID,
    original_id UUID,
    param_user_id UUID
) RETURNS VOID AS $$
BEGIN
    -- Insert a system message for each ticket indicating the SLA change
    INSERT INTO messages (type, ticket_id, author_id, content)
    SELECT
        'SYSTEM'::MessageType,
        t.id,
        param_user_id,
        'SYSTEM: SLA Migration'
    FROM Tickets t
    WHERE sla_id = original_id;

    -- Update the SLA ID of each ticket
    UPDATE tickets
    SET sla_id = replacement_id
    WHERE sla_id = original_id;

    -- Update the default SLA in the config table if it matches the original SLA
    IF EXISTS (
        SELECT 1
        FROM config
        WHERE original_id = (
            SELECT default_sla
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
            replacement_id,
            (
                SELECT default_severity
                FROM config
                ORDER BY created_at DESC
                LIMIT 1
            ),
            (
                SELECT default_assignee
                FROM config
                ORDER BY created_at DESC
                LIMIT 1
            )
        );
    END IF;

    -- Delete the original SLA
    DELETE FROM sla
    WHERE id = original_id;
END;
$$ LANGUAGE plpgsql;
