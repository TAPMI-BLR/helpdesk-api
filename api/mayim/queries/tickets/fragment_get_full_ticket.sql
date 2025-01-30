SELECT
    t.id,
    t.title,
    json_build_object(
        'id', u.id,
        'name', u.name,
        'email', u.email,
        'data', u.data,
        'is_team', (st.id IS NOT NULL),
        'is_sys_admin', st.is_sys_admin IS TRUE,
        'is_disabled', COALESCE(st.is_disabled, false)
    ) AS user,
    json_build_object(
        'id', sc.id,
        'name', sc.name,
        'category_id', sc.category_id,
        'category', row_to_json(c.*),
        'colour', sc.colour
    ) as subcategory,
    json_build_object(
        'id', a.id,
        'name', a.name,
        'email', a.email,
        'data', a.data,
        'is_team', (sa.id IS NOT NULL),
        'is_sys_admin', sa.is_sys_admin IS TRUE,
        'is_disabled', COALESCE(sa.is_disabled, false)
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
    Categories c ON sc.category_id = c.id
JOIN
    Severity sev ON t.severity_id = sev.id
JOIN
    SLA sla ON t.sla_id = sla.id
JOIN
    Users u ON t.user_id = u.id
LEFT JOIN
    Staff st ON u.id = st.id
JOIN
    Staff sa ON t.assignee_id = sa.id
JOIN
    Users a ON sa.id = a.id
