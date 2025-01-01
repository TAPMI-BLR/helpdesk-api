UPDATE
    tickets
SET
    ticket_status = 'OPEN',
    closed_at = NULL
WHERE
    id = $ticket_id;
