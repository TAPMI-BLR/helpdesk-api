INSERT INTO tickets (
        title,
        user_id,
        subcategory_id,
        assignee_id,
        severity_id,
        sla_id
    )
VALUES (
        $title,
        $user_id,
        $subcategory_id,
        $assignee_id,
        $severity,
        $sla
    )
RETURNING *;
