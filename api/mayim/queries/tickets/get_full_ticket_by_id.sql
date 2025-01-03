SELECT
    t.id,
    t.title,
    json_build_object(
        'id', u.id,
        'name', u.name,
        'email', u.email,
        'data', u.data,
        'is_team', (st.email IS NOT NULL),
        'is_sys_admin', st.is_sys_admin IS TRUE
    ) AS user,
    row_to_json(sc.*) AS subcategory,
    json_build_object(
        'id', a.id,
        'name', a.name,
        'email', a.email,
        'data', a.data,
        'is_team', (sa.email IS NOT NULL),
        'is_sys_admin', sa.is_sys_admin IS TRUE
    ) AS assignee,
    row_to_json(sev.*) AS severity,
    row_to_json(sla.*) AS sla,
    t.created_at,
    t.closed_at,
    t.resolution_status,
    t.ticket_status
FROM
    Tickets t
JOIN
    SubCategories sc ON t.subcategory_id = sc.id
JOIN
    Severity sev ON t.severity_id = sev.id
JOIN
    SLA sla ON t.sla_id = sla.id
LEFT JOIN
    Users u ON t.user_id = u.id
LEFT JOIN
    Staff st ON u.email = st.email
LEFT JOIN
    Staff sa ON t.assignee_id = sa.id
LEFT JOIN
    Users a ON sa.email = a.email
WHERE
    t.id = $ticket_id
