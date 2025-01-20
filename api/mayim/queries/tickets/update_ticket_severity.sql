UPDATE
    tickets
SET
    severity_id = $severity_id
WHERE
    id = $ticket_id;
