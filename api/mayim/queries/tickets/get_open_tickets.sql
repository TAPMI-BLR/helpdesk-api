SELECT * 
FROM tickets
WHERE ticket_status = "OPEN"
LIMIT $limit OFFSET $offset;