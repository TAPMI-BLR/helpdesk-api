UPDATE
    tickets
SET
    resolution_status = $resolution
WHERE
    id = $ticket_id;
