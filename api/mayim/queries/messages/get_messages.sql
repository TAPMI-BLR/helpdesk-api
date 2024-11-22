SELECT
    m.id,
    m.created_at,
    m.type,
    m.ticket_id,
    row_to_json((SELECT u FROM (SELECT u.id, u.name) u)) AS author,
    m.content,
    m.file_id
FROM
    messages m
JOIN
    users u ON u.id = m.author_id
WHERE
    m.ticket_id = $ticket_id
ORDER BY
    m.created_at DESC
LIMIT
    $limit OFFSET $offset;
