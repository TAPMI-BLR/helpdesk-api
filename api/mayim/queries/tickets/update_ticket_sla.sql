UPDATE
    tickets
SET
    sla_id = $sla_id
WHERE
    id = $ticket_id;
