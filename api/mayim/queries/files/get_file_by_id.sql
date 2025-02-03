SELECT f.* FROM messages m
JOIN files f ON m.file_id = f.id
WHERE m.ticket_id = $ticket_id AND m.file_id = $file_id;
