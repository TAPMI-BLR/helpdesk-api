UPDATE
    tickets
SET
    ticket_status = 'CLOSED',
    closed_at = NOW()
WHERE
    id = $ticket_id;
