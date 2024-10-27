SELECT *
FROM tickets
WHERE ticket_status = 'OPEN'
AND user_id = $user_id
LIMIT $limit OFFSET $offset;
