INSERT into config (
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
        ), $severity_id, (
            SELECT default_assignee
            FROM config
            ORDER BY created_at DESC
            LIMIT 1
        )
    );
