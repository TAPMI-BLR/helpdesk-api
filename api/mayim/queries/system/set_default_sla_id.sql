INSERT into config (
        default_sla,
        default_severity,
        default_assignee
    )
VALUES (
        $sla_id,
        (
            SELECT default_severity
            FROM config
            ORDER BY created_at DESC
            LIMIT 1
        ), (
            SELECT default_assignee
            FROM config
            ORDER BY created_at DESC
            LIMIT 1
        )
    );
