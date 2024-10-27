SELECT *
FROM messages
WHERE ticket_id = $ticket_id
ORDER BY created_at DESC
LIMIT $limit OFFSET $offset;
