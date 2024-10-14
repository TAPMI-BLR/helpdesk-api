SELECT *
FROM messages
WHERE ticket_id = $ticket_id
LIMIT $limit OFFSET $offset;